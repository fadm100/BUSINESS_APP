clear
clc

d1 = 83.7; % Diferencia entre punta y valle
d2 = 81.96; % Diferencia entre noche y valle

T_v = 0.2 % 20 centavos de dolar aproximadamente 820 COP

T_n = -(d2-200)*T_v/(d2+200)
T_p = -(d1+200)*T_v/(d1-200)