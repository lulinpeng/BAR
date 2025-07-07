import math
def print_big_num(n:int, name:str, formule:str):
    print(f'{name} = {n}')
    print(f'{name}_hex = {hex(n)}')
    print(f'{math.ceil(math.log2(abs(n)))} bit, {formule}\n')
    return

z_hex = '-0xd201000000010000' # Section 2.1 https://eprint.iacr.org/2019/403.pdf
z = int(z_hex, 16)
print_big_num(z, 'z', 'z = z')

r = z*z*z*z - z*z + 1
r_hex = hex(r)
print_big_num(r, 'r', 'r = z^4 - z^2 + 1')

q = ((z - 1) * (z - 1) * r + z) // 3
q_hex = hex(q)
print_big_num(q, 'q', 'q = (z - 1)^2 * r / 3')

# z = -15132376222941642752
# z_hex = -0xd201000000010000
# 64 bit, z = z

# r = 52435875175126190479447740508185965837690552500527637822603658699938581184513
# r_hex = 0x73eda753299d7d483339d80809a1d80553bda402fffe5bfeffffffff00000001
# 255 bit, r = z^4 - z^2 + 1

# q = 4002409555221667393417789825735904156556882819939007885332058136124031650490837864442687629129025752288709566988288
# q_hex = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb154000045ffaaaaaaab0000
# 381 bit, q = (z - 1)^2 * r / 3
