#include "KeyboardComponent.h"

KeyboardComponent::KeyboardComponent(juce::MidiKeyboardState& state)
    : keyboard(state, juce::MidiKeyboardComponent::horizontalKeyboard)
{
    addAndMakeVisible(keyboard);
}

void KeyboardComponent::resized()
{
    keyboard.setBounds(getLocalBounds());
}
