
#pragma once
#include <JuceHeader.h>
#include "SeedManager.h"

class SeedComponent : public juce::Component
{
public:
    SeedComponent(SeedManager& manager);
    ~SeedComponent() override = default;

    void paint(juce::Graphics& g) override;
    void resized() override;

private:
    SeedManager& manager;
    juce::Label seedLabel;
    juce::TextButton generateButton;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(SeedComponent)
};
