#pragma once
#include <JuceHeader.h>

class OscillatorComponent : public juce::Component, private juce::Timer
{
public:
    OscillatorComponent();
    void paint(juce::Graphics&) override;
    void setSample(float newSample);

private:
    void timerCallback() override;

    juce::Array<float> waveform;
    const int bufferSize = 512;
};
