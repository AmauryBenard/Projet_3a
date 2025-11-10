#pragma once
#include <JuceHeader.h>

class FilterComponent : public juce::Component
{
public:
    void paint(juce::Graphics&) override;
    void updateFilter(juce::dsp::IIR::Coefficients<float>::Ptr coeff, double sampleRate);

private:
    std::vector<float> mags;
    juce::dsp::IIR::Coefficients<float>::Ptr coeffs;
    double sr = 44100.0;
};
