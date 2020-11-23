function blinkLED() %#codegen

% Create a Raspberry Pi object
r= raspi('192.168.1.114','pi','softwareFYE20');

% Blink the LED for 100 cycles
for count = 1:100
    % Turn on the LED
    writeLED(r,'LED0', 1);
    % Pause for 0.5 seconds
    system(r, 'sleep 0.5');
    % Turn off the LED
    writeLED(r,'LED0', 0);
    % Pause for 0.5 seconds
    system(r, 'sleep 0.5');
end
end