#include "SeedComponent.h"

SeedComponent::SeedComponent(SeedManager& m) : manager(m)
{
    addAndMakeVisible(seedLabel);
    seedLabel.setText("Seed: " + manager.getSeedString(), juce::dontSendNotification);
    seedLabel.setJustificationType(juce::Justification::centred);
    seedLabel.setFont(juce::Font(16.0f));

    addAndMakeVisible(generateButton);
    generateButton.setButtonText("Generate Seed");
    generateButton.onClick = [this]()
        {
            manager.generateNewSeed();
            seedLabel.setText("Seed: " + manager.getSeedString(), juce::dontSendNotification);
        };
}

void SeedComponent::paint(juce::Graphics& g)
{
    g.fillAll(juce::Colours::black);
    g.setColour(juce::Colours::aqua);
    g.drawRect(getLocalBounds(), 2);
}

void SeedComponent::resized()
{
    auto area = getLocalBounds().reduced(10);
    seedLabel.setBounds(area.removeFromTop(30));
    generateButton.setBounds(area.removeFromTop(30));
}
