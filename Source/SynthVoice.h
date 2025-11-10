#pragma once
#include <JuceHeader.h>
#include "SynthSound.h"
#include "EnvelopeComponent.h"

class SynthVoice : public juce::SynthesiserVoice
{
public:
    SynthVoice();

    bool isNoteActive() const { return adsr.isActive(); }

    bool canPlaySound(juce::SynthesiserSound* sound) override
    {
        return dynamic_cast<SynthSound*> (sound) != nullptr;
    }

    void setEnvelopeFromComponent(const EnvelopeComponent& env)
    {
        adsr.setParameters(env.getADSRParams());
    }

    void startNote(int midiNoteNumber, float velocity, juce::SynthesiserSound*, int) override;
    void stopNote(float, bool allowTailOff) override;
    void pitchWheelMoved(int) override {}
    void controllerMoved(int, int) override {}
    void renderNextBlock(juce::AudioBuffer<float>&, int startSample, int numSamples) override;

    void setOscType(int type) { oscType = type; } // 0=sine,1=saw,2=square,3=triangle
    float getVisualSample() const noexcept { return lastSample; }

    void setFilterType(int type);
    void setFilterCutoff(float newCutoff);
    void setFilterResonance(float newResonance);

    void prepareToPlay(double newSampleRate, int samplesPerBlock, int outputChannels);

    void updateFilter();


    juce::dsp::IIR::Coefficients<float>::Ptr getFilterCoefficients() { return filter.coefficients; }
    juce::ADSR::Parameters getADSRParameters() const { return adsrParams; }

    

private:

    int blockSize = 0;

    double sampleRate = 44100.0;
    double phase = 0.0;
    double frequency = 440.0;
    float level = 0.0f;
    int oscType = 0;
    float lastSample = 0.0f;



    juce::ADSR adsr;
    juce::ADSR::Parameters adsrParams{ 0.01f, 0.2f, 0.8f, 0.3f };

    juce::dsp::IIR::Filter<float> filter;
    juce::dsp::IIR::Coefficients<float>::Ptr filterCoeffs;

    int filterType = 0; // 0 = LP, 1 = HP, 2 = BP
    float cutoff = 1000.0f;
    float resonance = 0.7f;
};
