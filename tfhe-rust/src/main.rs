use tfhe::prelude::*;
use tfhe::{generate_keys, set_server_key, ConfigBuilder, FheUint32, FheUint8, ClientKey, ServerKey};
use chrono::Local;
use std::fs;
use serde::{Serialize, de::DeserializeOwned};
use std::path::Path;
use anyhow::{Result, Context};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let clear_a = 1344u32;
    let clear_b = 5u32;
    let clear_c = 7u8;
    println!("+++ Target: min((a * b) >> b, c) & 1 = min(({} + {}) >> {}, {}) & 1 +++", clear_a, clear_b, clear_b, clear_c);
    
    let config = ConfigBuilder::default().build();

    // ********** client side ************
    println!("{} 1. key generation ...", now());
    let (client_key, server_keys) = generate_keys(config);
    println!("{} 2. save keys into files ...", now());
    serialize_to_file(&client_key, "client_key.bin")?;
    serialize_to_file(&server_keys, "server_key.bin")?;
    
    println!("{} 2. encrypting ...", now());
    println!("{}    2.1 a -> [a]", now());
    let encrypted_a = FheUint32::try_encrypt(clear_a, &client_key)?;
    println!("{}    2.2 b -> [b]", now());
    let encrypted_b = FheUint32::try_encrypt(clear_b, &client_key)?;
    println!("{}    2.3 c -> [c]", now());
    let encrypted_c = FheUint8::try_encrypt(clear_c, &client_key)?;
    println!("{}    2.4 save ciphertexts into files", now());
    serialize_to_file(&encrypted_a, "encrypted_a.bin")?;
    serialize_to_file(&encrypted_b, "encrypted_b.bin")?;
    serialize_to_file(&encrypted_c, "encrypted_c.bin")?;

    println!("{} 3. homomorhpic evaluation ...", now());
    // ********** server side ************
    let server_keys: ServerKey = deserialize_from_file("server_key.bin")?;
    let mut encrypted_a: FheUint32 = deserialize_from_file("encrypted_a.bin")?;
    let encrypted_b: FheUint32 = deserialize_from_file("encrypted_b.bin")?;
    let encrypted_c: FheUint8 = deserialize_from_file("encrypted_c.bin")?;
    
    set_server_key(server_keys);
    println!("{}    3.1 [x] * [y]", now());
    let encrypted_res_mul = &encrypted_a * &encrypted_b;
    println!("{}    3.2 [x] >> [y] ", now());
    encrypted_a = &encrypted_res_mul >> &encrypted_b;
    let casted_a: FheUint8 = encrypted_a.cast_into();
    println!("{}    3.4 min([x], [y])", now());
    let encrypted_res_min = &casted_a.min(&encrypted_c);
    println!("{}    3.5 [x] & 1", now());
    let encrypted_res = encrypted_res_min & 1_u8;

    serialize_to_file(&encrypted_res, "encrypted_res.bin")?;

    // ********** client side ************
    let client_key: ClientKey = deserialize_from_file("client_key.bin")?;
    let encrypted_res: FheUint8 = deserialize_from_file("encrypted_res.bin")?;
    println!("{} 4. decrypting", now());
    let clear_res: u8 = encrypted_res.decrypt(&client_key);
    println!("{} result: {}", now(), clear_res);
    assert_eq!(clear_res, 1_u8);

    Ok(())
}

fn now() -> String {
    Local::now().format("%H:%M:%S").to_string()
}

fn serialize_to_file<T: Serialize>(data: &T, file_path: &str) -> Result<()> {
    let bytes = bincode::serialize(data)
        .with_context(|| format!("failed to serialize data: {}", file_path))?;
    fs::write(file_path, &bytes)
        .with_context(|| format!("failed to write info file: {}", file_path))?;
    
    Ok(())
}

fn deserialize_from_file<T: DeserializeOwned>(file_path: &str) -> Result<T> {
    if !Path::new(file_path).exists() {
        anyhow::bail!("file not found: {}", file_path);
    }

    let bytes = fs::read(file_path)
        .with_context(|| format!("failed to read file: {}", file_path))?;
    
    let data: T = bincode::deserialize(&bytes)
        .with_context(|| format!("failed to deserialize data: {}", file_path))?;
    
    Ok(data)
}