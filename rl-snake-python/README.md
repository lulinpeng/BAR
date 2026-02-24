# INTRO
Reinforcement Learning.

# ENV
```shell
# Python 3.9.6
pip install -r requirements.txt
```

# RUN
```shell
# q-table training
python3 main.py --gui 0 --episodes 1000 --mode train --engine qtable

# q-network training
python3 main.py --gui 0 --episodes 1000 --mode train --engine qnetwork


# test
python3 main.py --gui 1 --episodes 10 --mode test --engine qtable --model models/20240324_174254_q_table_snake.pkl

python3 main.py --gui 1 --episodes 10 --mode test --engine qnetwork --model models/20240324_174354_q_network_snake.pkl

# human playing
python3 snakegame.py
```