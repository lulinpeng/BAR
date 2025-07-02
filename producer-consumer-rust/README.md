# Version
```shell
rustc --version
# rustc 1.89.0
cargo --version
# cargo 1.89.0
```
# Build and Run
```shell
cd producer-consumer-rust/
cargo run
```
## Result
```
Consumed: ID: 0, Name: apple
Produced: 0
Produced: 1
Produced: 2
Consumed: ID: 1, Name: orange
Consumed: ID: 2, Name: pineapple
Produced: 3
Produced: 4
Consumed: ID: 3, Name: watermelon
Produced: 5
Consumed: ID: 4, Name: apple
Produced: 6
Consumed: ID: 5, Name: orange
Produced: 7
Produced: 8
Produced: 9
Producer exit
Consumed: ID: 6, Name: pineapple
Consumed: ID: 7, Name: watermelon
Consumed: ID: 8, Name: apple
Consumed: ID: 9, Name: orange
Receiver exit
```
