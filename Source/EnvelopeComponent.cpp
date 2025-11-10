#include "EnvelopeComponent.h"

EnvelopeComponent::EnvelopeComponent()
{
    setADSR(0.01f, 0.1f, 0.8f, 0.2f); // valeurs par d	faut
}

void EnvelopeComponent::setADSR(float a, float d, float s, float r)
{
    adsrParams.attack = a;
    adsrParams.decay = d;
    adsrParams.sustain = s;
    adsrParams.release = r;

    // recalculer la forme statique
    envelopePath.clear();
    auto area = getLocalBounds().toFloat();
    float width = area.getWidth();
    float height = area.getHeight();

    float x0 = 0.0f;
    float y0 = height;
    float xA = width * a;
    float yA = 0.0f;
    float xD = xA + width * d;
    float yD = height * (1.0f - s);
    float xS = xD + width * 0.2f; // sustain hold
    float xR = width;

    envelopePath.startNewSubPath(x0, y0);
    envelopePath.lineTo(xA, yA);  // attack
    envelopePath.lineTo(xD, yD);  // decay
    envelopePath.lineTo(xS, yD);  // sustain
    envelopePath.lineTo(xR, height); // release

    repaint();
}

void EnvelopeComponent::startEnvelopeVisual()
{
    visualActive = true;
    repaint();
}

void EnvelopeComponent::stopEnvelopeVisual()
{
    visualActive = false;
    repaint();
}


void EnvelopeComponent::paint(juce::Graphics& g)
{
    g.fillAll(juce::Colours::darkgrey);

    g.setColour(juce::Colours::white);
    g.strokePath(envelopePath, juce::PathStrokeType(2.0f));

    if (visualActive)
    {
        // possibilit	 d'ajouter un point anim	 repr	sentant la progression de l'enveloppe
    }
}

