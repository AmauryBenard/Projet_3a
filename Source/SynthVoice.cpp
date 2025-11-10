#include "SynthVoice.h"

SynthVoice::SynthVoice()
{
    setFilterType(0); // low-pass par d	faut
}

void SynthVoice::setFilterType(int type)
{
    filterType = juce::jlimit(0, 2, type);
    setFilterCutoff(cutoff);
}

void SynthVoice::setFilterCutoff(float freq)
{
    cutoff = freq;
    using Coeff = juce::dsp::IIR::Coefficients<float>;
    switch (filterType)
    {
    case 0:
        filter.coefficients = Coeff::makeLowPass(sampleRate, cutoff, resonance);
        break;
    case 1:
        filter.coefficients = Coeff::makeHighPass(sampleRate, cutoff, resonance);
        break;
    case 2:
        filter.coefficients = Coeff::makeBandPass(sampleRate, cutoff, resonance);
        break;
    }
}

void SynthVoice::setFilterResonance(float q)
{
    resonance = q;
    setFilterCutoff(cutoff);
}

void SynthVoice::startNote(int midiNoteNumber, float velocity,
    juce::SynthesiserSound*, int)
{
    frequency = juce::MidiMessage::getMidiNoteInHertz(midiNoteNumber);
    level = velocity;
    phase = 0.0;
    adsr.setParameters(adsrParams);
    adsr.noteOn();
}

void SynthVoice::stopNote(float, bool allowTailOff)
{
    adsr.noteOff();
    if (!allowTailOff || !adsr.isActive())
        clearCurrentNote();
}

void SynthVoice::renderNextBlock(juce::AudioBuffer<float>& buffer, int startSample, int numSamples)
{
    auto* left = buffer.getWritePointer(0, startSample);
    auto* right = buffer.getNumChannels() > 1 ? buffer.getWritePointer(1, startSample) : nullptr;

    for (int i = 0; i < numSamples; ++i)
    {
        float oscSample = 0.0f;
        float increment = frequency / sampleRate;
        phase += increment;
        if (phase >= 1.0) phase -= 1.0;

        switch (oscType)
        {
        case 0: oscSample = std::sin(2.0 * juce::MathConstants<double>::pi * phase); break;
        case 1: oscSample = 2.0f * (float)phase - 1.0f; break; // saw
        case 2: oscSample = (phase < 0.5 ? 1.0f : -1.0f); break; // square
        case 3: oscSample = 2.0f * std::abs(2.0f * (float)phase - 1.0f) - 1.0f; break; // triangle
        }

        float envSample = adsr.getNextSample();
        float sample = oscSample * level * envSample;
        sample = filter.processSample(sample);

        lastSample = sample; // pour visualisation

        left[i] += sample;
        if (right) right[i] += sample;
    }
}


void SynthVoice::updateFilter()
{
    // si tu veux juste actualiser les coefficients :
    //filter.prepare({ getSampleRate(), (juce::uint32)getBlockSize(), 1 });
}



// Assurez-vous que prepareToPlay est appel	 avant le traitement audio
void SynthVoice::prepareToPlay(double newSampleRate, int samplesPerBlock, int outputChannels)
{

    this->blockSize = samplesPerBlock;
    sampleRate = newSampleRate;

    juce::dsp::ProcessSpec spec;
    spec.sampleRate = sampleRate;
    spec.maximumBlockSize = samplesPerBlock;
    spec.numChannels = outputChannels;

    filter.prepare(spec);
    updateFilter();
}


void SynthVoice::setOscType(int type) { oscType = juce::jlimit(0, 3, type); }
void SynthVoice::setADSR(float a, float d, float s, float r)
{
    adsrParams.attack = a;
    adsrParams.decay = d;
    adsrParams.sustain = s;
    adsrParams.release = r;
    adsr.setParameters(adsrParams);
}