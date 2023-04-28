st1 = 'play, home, work'
st2 = 'играть, дом, работа'
st1 = st1.split(', ')
st2 = st2.split(', ')
final = ''
for i in range(len(st1)):
    final += f'{st1[i]} - {st2[i]}\n'
print(final)


print('նրանք; նրա; հաշվապահություն; մասին'.split('; '))