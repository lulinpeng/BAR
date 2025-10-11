use serde::{Deserialize, Serialize};
use std::thread;
use std::{error::Error, sync::mpsc};
use tokio::time::Duration;
mod logger;

#[derive(Debug, Serialize, Clone)]
pub struct RpcReq {
    pub name: String,
    pub id: i32,
}

#[derive(Debug, Deserialize, Clone)]
pub struct RpcResp {
    pub name: String,
    pub time: String,
    pub id: i32,
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let _guard = logger::setup_logger("info", "/tmp/demo/", "demo.log");
    let url = "http://127.0.0.1:5000/demo";
    let timeout: u64 = 10;
    let channel_size: usize = 10;
    let (tx, rx) = mpsc::sync_channel(channel_size);

    let producer = thread::spawn(move || {
        let client = reqwest::blocking::Client::new();
        let mut cnt: u64 = 0;
        loop {
            let request = RpcReq {
                name: "demo".to_string(),
                id: cnt as i32 + 1,
            };
            match client
                .post(url)
                .header("Content-Type", "application/json")
                .json(&request)
                .timeout(Duration::from_secs(timeout))
                .send()
            {
                Ok(resp) => {
                    let status = resp.status();
                    tracing::info!("producer: status {:?}", status);
                    if status.is_success() {
                        match resp.json::<RpcResp>() {
                            Ok(resp_json) => {
                                tracing::info!("producer: send {}-th request", cnt);
                                cnt += 1;
                                match tx.send(resp_json) {
                                    Ok(result) => tracing::info!(
                                        "producer: tx send channel success, result {:?}",
                                        result
                                    ),

                                    Err(e) => {
                                        tracing::error!(
                                            "producer: tx send channel error, details: {:?}",
                                            e
                                        )
                                    }
                                }
                            }
                            Err(e) => {
                                tracing::info!("producer: error response json, details: {:?}", e)
                            }
                        }
                    } else {
                        tracing::error!("producer: request failed with status: {}", status);
                    }
                }
                Err(e) => {
                    tracing::error!("producer: heerer {:?}", e);
                }
            };
        }
    });

    let consumer = thread::spawn(move || {
        let mut cnt: u64 = 0;
        loop {
            match rx.recv() {
                Ok(resp) => {
                    tracing::info!("consumer: recv {}-th response: {:?}", cnt, resp);
                    cnt += 1;
                    thread::sleep(Duration::from_millis(3000));
                }
                Err(e) => {
                    tracing::error!("consumer: error details: {:?}", e);
                }
            }
        }
    });
    producer.join().unwrap();
    consumer.join().unwrap();
    Ok(())
}
