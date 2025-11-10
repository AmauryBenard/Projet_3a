#include "OscillatorComponent.h"

OscillatorComponent::OscillatorComponent()
{
    waveform.ensureStorageAllocated(bufferSize);
    startTimerHz(60);
}

void OscillatorComponent::setSample(float newSample)
{
    waveform.add(newSample);
    if (waveform.size() > bufferSize)
        waveform.remove(0);
}

void OscillatorComponent::timerCallback()
{
    repaint();
}

void OscillatorComponent::paint(juce::Graphics& g)
{
    g.fillAll(juce::Colours::black);
    g.setColour(juce::Colours::white);

    auto area = getLocalBounds().toFloat();
    if (waveform.size() < 2) return;

    juce::Path path;
    path.startNewSubPath(area.getX(), area.getCentreY());

    for (int i = 0; i < waveform.size(); ++i)
    {
        float x = area.getX() + (i / (float)bufferSize) * area.getWidth();
        float y = area.getCentreY() - waveform[i] * area.getHeight() * 0.4f;
        if (i == 0) path.startNewSubPath(x, y);
        else path.lineTo(x, y);
    }

    g.strokePath(path, juce::PathStrokeType(2.0f));
}
