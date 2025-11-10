#pragma once
#include <JuceHeader.h>

class LFOComponent : public juce::Component
{
public:
    LFOComponent() = default;
    ~LFOComponent() override = default;

    void paint(juce::Graphics& g) override;
    void resized() override;
};
