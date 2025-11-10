#pragma once
#include <JuceHeader.h>

class KeyboardComponent : public juce::Component
{
public:
    KeyboardComponent(juce::MidiKeyboardState& state);
    void resized() override;

private:
    juce::MidiKeyboardComponent keyboard;
};
