use rand::Rng;
use std::sync::mpsc; // multiple producer, single consumer
use std::thread;
use std::time::Duration;
mod product;

fn main() {
    // create a sync channel
    let buffer_size = 3;
    let (tx, rx) = mpsc::sync_channel(buffer_size);

    // start producer thread
    let producer = thread::spawn(move || {
        let mut rng = rand::rng();
        for i in 0..10 {
            // send to channel
            let name = match i % 4 {
                0 => "apple",
                1 => "orange",
                2 => "pineapple",
                3 => "watermelon",
                _ => unreachable!(),
            };
            let prod = product::Product::new(i, name);
            tx.send(prod).unwrap(); // block when buffer is full
            let sleep_time = Duration::from_millis(rng.random_range(100..800)); // random sleep
            thread::sleep(sleep_time);
            println!("Produced: {}", i);
        }
        println!("Producer exit")
    });

    // start consumer thread
    let consumer = thread::spawn(move || {
        let mut rng = rand::rng();
        loop {
            match rx.recv() {
                // block when buffer is empty
                Ok(prod) => {
                    let sleep_time = Duration::from_millis(rng.random_range(500..800)); // random sleep
                    thread::sleep(sleep_time);
                    println!("Consumed: {}", prod);
                }
                Err(_) => {
                    println!("Receiver exit");
                    break;
                }
            }
        }
    });

    producer.join().unwrap();
    consumer.join().unwrap();
}
