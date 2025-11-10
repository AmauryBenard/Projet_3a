#pragma once
#include <JuceHeader.h>

class EnvelopeComponent : public juce::Component
{
public:
    EnvelopeComponent();

    // Set ADSR parameters
    void setADSR(float a, float d, float s, float r);

    // Get ADSR parameters
    juce::ADSR::Parameters getADSRParams() const { return adsrParams; }

    // For visualisation
    void startEnvelopeVisual();
    void stopEnvelopeVisual();

    void paint(juce::Graphics& g) override;

private:
    juce::ADSR::Parameters adsrParams{ 0.01f, 0.1f, 0.8f, 0.2f };
    juce::Path envelopePath;

    bool visualActive = false;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(EnvelopeComponent)
};
