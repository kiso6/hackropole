#!/usr/bin/python3


key = b"0ba883a22afb84506c8d8fd9e42a5ce4e8eb1cc87c315a28dd"
encflag = bytes.fromhex("277b6b701a01005505075d0c53550555095d595e065c0402065407510055015e5557525b575c5154500751070b5e5551555602595a070502575152010f03570206015a500f1b6e")
flag = ""

for i in range(len(encflag)):
    flag += chr(encflag[i] ^ key[(i+2) % len(key)])

print(flag)
