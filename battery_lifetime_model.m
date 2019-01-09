%battery cycle service life model
%David Storelli
%10 October 2018

%Inputs
%load from Excel files
%{
load_profile = readtable('Profiles.xlsx','Sheet',1);
gen_profile = readtable('Profiles.xlsx','Sheet',2);
%}
%Battery configuration
battery_voltage = 12;
battery_capacity = 20;
%Model parameters
delta_t = 0.5;
SOC = zeros(length(gen_profile.time),1);
SOC(1) = 1;


%Calculation
for t = 1:(length(SOC)-1)
    I = (gen_profile.gen_energy(t+1)-load_profile.ld_energy(t+1))/battery_voltage;
    delta_SOC = I*delta_t/battery_capacity;
    
    if (SOC(t)+delta_SOC)>1
        SOC(t+1) = 1;
    else
        SOC(t+1) = SOC(t)+delta_SOC;
    end
end

figure
hold on
yyaxis left
plot(load_profile.time,load_profile.ld_energy);
plot(gen_profile.time,gen_profile.gen_energy);

yyaxis right 
axis([0,24,0,1.1]);
plot(gen_profile.time, SOC);
legend('load profile','gen profile','SOC')
hold off
