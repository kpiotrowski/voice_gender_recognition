<!-- Improved compatibility of back to top link: See:-->

<a name="readme-top"></a>

# Gender Voice Recognition in Python

This project is a fork of the original repository, which has been inactive for several years. My goal is to continue development and improve the functionality of voice gender recognition.

## Features
- **Real-time Gender Recognition**: The script captures audio from your microphone in real-time and determines the gender of the speaker.
- **Gender Recognition from Audio Samples**: The script can also process pre-recorded .wav audio files and determine the gender of the speaker.
- **Harmonic Product Spectrum (HPS)**: The script utilizes the HPS method for pitch (fundamental frequency) detection, a key factor in determining the gender of a speaker.

## How it Works
The script applies the HPS method to the input audio to detect the pitch of the speaker's voice. It then compares this pitch to predefined frequency ranges for male and female voices. If the pitch falls within the male frequency range, the script identifies the speaker as male. If the pitch falls within the female frequency range, the script identifies the speaker as female.

## Usage
The script is easy to use and can be run directly from the command line. It provides two modes of operation: real-time gender recognition using a microphone and gender recognition from .wav audio samples.

## Dependencies
The script depends on several Python libraries, including `sounddevice` for audio input, `numpy` for numerical operations, and `scipy` for Fast Fourier Transform (FFT) and .wav file processing.

<!-- ROADMAP -->

# Roadmap

- [x] **Initialize Repository**
  - [x] Add `readme.md` for project documentation.
  - [x] Implement "Back to Top" links for easier navigation.
  - [x] Create `requirements.txt` for managing project dependencies.

- [ ] **Repository Optimization**
  - [x] Organize and improve the content for better readability.
  - [ ] Enhance code quality and structure.
  
- [ ] **Complete Documentation**
  - [x] Provide comprehensive documentation for the entire project.
  - [ ] Include detailed explanations for each component and functionality.

- [x] **Microphone Gender Recognition**
  - [x] Implement basic microphone gender recognition functionality.
  - [ ] Improve recognition accuracy.
  - [ ] Address and fix any new bugs introduced during recognition enhancements.

- [x] **Microphone Gender Detail**
  - [ ] Extend functionality to provide additional gender details.
  - [x] Include features to capture and analyze gender information from microphone input.

- [x] **Audio File Gender Detail**
  - [x] Implement gender recognition for audio files.
  - [ ] Enhance file-based gender recognition for improved accuracy.
  

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>
