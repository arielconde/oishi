% y signal in time domain
% fs signal sampling rate
[y, fs] = wavread('sample_females.wav');

frame_size = 20; % in ms, STFT 15-25 ms frame size

N = (frame_size/1000) * fs; % number of samples per frame


% FFT size
% get the nearest power of 2,  greater than or equal to N
NFFT = 2^nextpow2(N);


% total number of samples in recording / samples per frame
NFRAMES = floor(length(y)/N);


% Process each frame
pitch_fs = zeros(1, NFRAMES);
voiced_pitch_freq = [];
for i=1:NFRAMES

    % get a frame (overlapping)
    % overlapping frames examples
    % frame 1: 1 to 160
    % frame 2: 80 to 240
    start_idx = (i-1)*N/2+1;        % if N = 160, start at 1
    end_idx = start_idx + N - 1;    % if N = 160, end at 160
    signal = y(start_idx:end_idx);  % get the signal frame, given the start and end


    % (Optional) apply hamming window
    w = hamming(N);
    signal = signal .* w;


    % Derive cepstrum
    complex_spectrum = fft(signal, NFFT);           % Note: matlab performs some adjustments if signal doenst fit FFT size
    power_spectrum = (abs(complex_spectrum)).^2;    % Zero padding can be used to match the signal size to FFT
    cepstrum = ifft(log(power_spectrum), NFFT);     % Ex. for signal size 160 and FFT size of 256, set signal index 161 to 256 to 0


    % Apply "HIGH TIME LIFTERING" liftering to get the pitch frequency
    % cepstrum is symmetric, half of the cepstral coffecicents are used
    half_cepstrum = cepstrum(1:length(cepstrum)/2);

    L = zeros(1, length(half_cepstrum)); % liftering window

    Lc = 15; % liftering cut off length, usually 15 or 20

    % set 1 as value of the liftering window from index Lc to end
    % this creates a rectangular window
    L(Lc:length(L)) = 1;


    % High Time liftered cepstrum
    % perform matrix multiplication of the half_cepstrum and liftering window
    % get the real values
    ht_cepstrum = real(half_cepstrum .* L'); % L' transposes the liftering window (matrix)
     
    % Finally, get the pitch frequecy
    [val, idx] = max(ht_cepstrum); % val peak value, idx index of peak of the cepstrum
    pitch_frequency = fs/idx;
    
    % assign to array of pitch frequencies
    pitch_fs(i) = pitch_frequency;

    % Simple Voice Activity detection
    if mean(power_spectrum) >= 1 % an experimental value, most likely to fail on other inputs
        voiced_pitch_freq(length(voiced_pitch_freq)+1) = pitch_frequency; % record frames identified as voiced
    end

end

% Simple identification of gender
final_pitch_freq = mean(voiced_pitch_freq);

text = sprintf('Pitch Frequency is %f', final_pitch_freq);
disp(text);

if 165 <= final_pitch_freq && final_pitch_freq <= 180
    disp('In between'); % improvement - run other form of comparison
elseif 85 <= final_pitch_freq && final_pitch_freq <= 164
    disp('Male');
elseif 181 <= final_pitch_freq && final_pitch_freq <= 255
    disp('Female');
else
    disp('Not within the range of male or female pitch frequency');
end









