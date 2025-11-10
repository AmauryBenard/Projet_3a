#pragma once
#include <JuceHeader.h>
#include "SeedManager.h"
#include "SeedComponent.h"
#include "KeyboardComponent.h"
#include "SynthVoice.h"
#include "SynthSound.h"
#include "OscillatorComponent.h"
#include "FilterComponent.h"

#include "EnvelopeComponent.h"



class MainComponent : public juce::AudioAppComponent
{
public:
    MainComponent();
    ~MainComponent() override;

    void prepareToPlay(int samplesPerBlockExpected, double sampleRate) override;
    void getNextAudioBlock(const juce::AudioSourceChannelInfo& bufferToFill) override;
    void releaseResources() override;

    void paint(juce::Graphics& g) override;
    void resized() override;

private:


    double currentSampleRate = 44100.0;   // correct, car dans la classe


    SeedManager seedManager;
    SeedComponent seedComponent;
    juce::MidiKeyboardState keyboardState;
    KeyboardComponent keyboardComponent;
    OscillatorComponent oscDisplay;
    FilterComponent filterDisplay;
    EnvelopeComponent envelopeDisplay;

    // synth
    juce::Synthesiser synth;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(MainComponent)
};
