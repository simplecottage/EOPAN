import numpy as np
import pyaudio
import time
import threading
import keyboard
import matplotlib.pyplot as plt
from scipy.io import wavfile

class HearingTest:
    def __init__(self):
        self.frequencies = [250, 500, 1000, 2000, 3000, 4000, 6000, 8000]
        self.volume_start = -75
        self.volume_step = 1
        self.sample_rate = 44100
        
        # PyAudio setup
        self.p = pyaudio.PyAudio()
        self.stream = None
        
        # Results storage
        self.results = {
            'left': {},
            'right': {}
        }
        
    def generate_sine_wave(self, frequency, duration=1.0, volume_db=-20):
        """Generate a sine wave of specified frequency, duration and volume"""
        # Convert dB to amplitude
        amplitude = 10 ** (volume_db / 20)
        
        # Generate time array
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        
        # Generate sine wave
        sine_wave = amplitude * np.sin(2 * np.pi * frequency * t)
        
        # Convert to 32-bit float
        audio = sine_wave.astype(np.float32)
        
        return audio
    
    def play_tone(self, frequency, ear, volume_db):
        """Play a tone at the specified frequency, ear and volume"""
        # Generate the sine wave
        tone = self.generate_sine_wave(frequency, duration=0.1, volume_db=volume_db)  # Reduced to 0.1 seconds
        
        # Create stereo sound (left or right channel)
        stereo = np.zeros((len(tone), 2), dtype=np.float32)
        
        if ear == 'left':
            stereo[:, 0] = tone  # Left channel
        else:
            stereo[:, 1] = tone  # Right channel
            
        # Flatten for PyAudio
        stereo_flat = stereo.flatten()
        
        # Open stream if not already open
        if self.stream is None or not self.stream.is_active():
            self.stream = self.p.open(
                format=pyaudio.paFloat32,
                channels=2,
                rate=self.sample_rate,
                output=True
            )
        
        # Play the tone
        self.stream.write(stereo_flat.tobytes())
    
    def test_frequency(self, frequency, ear):
        """Test a specific frequency for a specific ear"""
        print(f"\nTesting {ear} ear at {frequency} Hz")
        print("Press SPACE when you hear the tone...")
        
        heard = False
        current_volume = self.volume_start
        
        while not heard and current_volume < -10:
            # Play tone
            self.play_tone(frequency, ear, current_volume)
            
            # Check if space was pressed during the tone
            start_time = time.time()
            while time.time() - start_time < 0.15:  # Wait just slightly longer than the tone
                if keyboard.is_pressed('space'):
                    heard = True
                    break
                time.sleep(0.01)
            
            if heard:
                break
                
            # Increase volume
            current_volume += self.volume_step
            print(f"Volume: {current_volume} dB")
        
        # Store result
        if heard:
            self.results[ear][frequency] = current_volume
            print(f"Threshold for {frequency} Hz in {ear} ear: {current_volume} dB")
        else:
            self.results[ear][frequency] = None
            print(f"Couldn't detect tone at maximum volume")
        
        # Small pause between tests
        time.sleep(1)

    def run_test(self):
        """Run the complete hearing test"""
        print("DIY Hearing Test")
        print("================")
        print("This test will play tones at different frequencies.")
        print("Press SPACE as soon as you hear each tone.")
        print("Make sure your headphones are correctly positioned (L/R).")
        print("\nPress ENTER to start the test...")
        
        keyboard.wait('enter')
        
        # Test each ear at each frequency
        for ear in ['left', 'right']:
            print(f"\n--- Testing {ear.upper()} ear ---")
            time.sleep(1)
            
            for freq in self.frequencies:
                self.test_frequency(freq, ear)
        
        # Close the stream
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
        
        self.p.terminate()
        
        # Show results
        self.plot_results()
    
    def plot_results(self):
        """Plot the audiogram from the test results"""
        plt.figure(figsize=(10, 6))
        
        # Plot for each ear
        markers = {'left': 'o', 'right': 'x'}
        colors = {'left': 'blue', 'right': 'red'}
        
        for ear in ['left', 'right']:
            # Get the frequencies and thresholds
            freqs = []
            thresholds = []
            
            for freq in self.frequencies:
                if freq in self.results[ear] and self.results[ear][freq] is not None:
                    freqs.append(freq)
                    thresholds.append(self.results[ear][freq])
            
            if freqs:  # Only plot if we have data
                plt.plot(freqs, thresholds, marker=markers[ear], color=colors[ear], 
                         label=f'{ear.capitalize()} Ear', linestyle='-')
        
        # Invert y-axis as audiograms show hearing loss as negative values
        plt.gca().invert_yaxis()
        
        # Logarithmic x-axis for frequencies
        plt.xscale('log')
        plt.xticks(self.frequencies, [str(f) for f in self.frequencies])
        
        # Labels and title
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Hearing Level (dB)')
        plt.title('DIY Audiogram')
        plt.grid(True)
        plt.legend()
        
        # Save the plot
        plt.savefig('audiogram_results.png')
        
        print("\nTest complete! Results saved as 'audiogram_results.png'")
        print("\nYour results (dB):")
        for ear in ['left', 'right']:
            print(f"\n{ear.upper()} EAR:")
            for freq in self.frequencies:
                if freq in self.results[ear] and self.results[ear][freq] is not None:
                    print(f"  {freq} Hz: {self.results[ear][freq]} dB")
                else:
                    print(f"  {freq} Hz: Not detected")

if __name__ == "__main__":
    # Create and run the test
    test = HearingTest()
    test.run_test()
