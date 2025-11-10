#include "FilterComponent.h"

void FilterComponent::updateFilter(juce::dsp::IIR::Coefficients<float>::Ptr c, double sampleRate)
{
    coeffs = c;
    sr = sampleRate;
    repaint();
}

void FilterComponent::paint(juce::Graphics& g)
{


    g.fillAll(juce::Colours::darkgrey);
    if (coeffs == nullptr) return;

    const int N = 256;
    mags.resize(N);

    float b0 = coeffs->coefficients[0];
    float b1 = coeffs->coefficients[1];
    float b2 = coeffs->coefficients[2];
    float a0 = coeffs->coefficients[3];
    float a1 = coeffs->coefficients[4];
    float a2 = coeffs->coefficients[5];

    for (int i = 0; i < N; ++i)
    {
        float omega = juce::MathConstants<float>::pi * i / (float)N;
        std::complex<float> z = std::exp(std::complex<float>(0, -omega));
        std::complex<float> num = b0 + b1 * z + b2 * z * z;
        std::complex<float> den = a0 + a1 * z + a2 * z * z;
        mags[i] = 20.0f * std::log10(std::abs(num / den) + 1e-12f);
    }

    auto area = getLocalBounds().toFloat();
    juce::Path p;
    for (int i = 0; i < N; ++i)
    {
        float x = (float)i / (N - 1) * area.getWidth();
        float y = juce::jmap(mags[i], -40.0f, 10.0f, area.getBottom(), area.getY());
        if (i == 0) p.startNewSubPath(x, y);
        else p.lineTo(x, y);
    }

    g.setColour(juce::Colours::white);
    g.strokePath(p, juce::PathStrokeType(1.5f));
}
