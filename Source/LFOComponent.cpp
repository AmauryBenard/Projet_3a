#include "LFOComponent.h"

void LFOComponent::paint(juce::Graphics& g)
{
    g.fillAll(juce::Colours::black);
    g.setColour(juce::Colours::aqua);
    g.drawText("LFO", getLocalBounds(), juce::Justification::centred);
}

void LFOComponent::resized()
{
    // Pour l’instant rien à redimensionner
}
