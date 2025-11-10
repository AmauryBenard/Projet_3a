#include "MainComponent.h"

MainComponent::MainComponent()
    : seedComponent(seedManager),
    keyboardComponent(keyboardState)
{

    setSize(800, 600); // largeur x hauteur par défaut


    addAndMakeVisible(seedComponent);
    addAndMakeVisible(keyboardComponent);
    addAndMakeVisible(oscDisplay);
    addAndMakeVisible(filterDisplay);
    addAndMakeVisible(envelopeDisplay);



    // initialiser le synth : ajouter sound + voices
    synth.clearSounds();
    synth.addSound(new SynthSound());
    const int numVoices = 8;
    for (int i = 0; i < numVoices; ++i)
        synth.addVoice(new SynthVoice());

    // démarrer l'audio (0 in, 2 out)
    setAudioChannels(0, 2);
}

MainComponent::~MainComponent()
{
    shutdownAudio();
}

void MainComponent::prepareToPlay(int samplesPerBlockExpected, double sampleRate)
{
    juce::ignoreUnused(samplesPerBlockExpected);
    currentSampleRate = sampleRate;
    // informer le synth du sample rate courant
    synth.setCurrentPlaybackSampleRate(sampleRate);
}

void MainComponent::getNextAudioBlock(const juce::AudioSourceChannelInfo& bufferToFill)
{
    // clear le buffer de sortie
    bufferToFill.clearActiveBufferRegion();

    // construire un MidiBuffer à partir du keyboardState
    juce::MidiBuffer incomingMidi;
    keyboardState.processNextMidiBuffer(incomingMidi, bufferToFill.startSample, bufferToFill.numSamples, true);

    // faire sonner le synth dans le buffer de sortie
    synth.renderNextBlock(*bufferToFill.buffer, incomingMidi, bufferToFill.startSample, bufferToFill.numSamples);

    auto params = seedManager.getMappedParameters();

    // récupérer la première voice active pour la visu
    for (int i = 0; i < synth.getNumVoices(); ++i)
    {
        if (auto* v = dynamic_cast<SynthVoice*>(synth.getVoice(i)))
        {
            v->prepareToPlay(currentSampleRate, 512, 2);
            //oscDisplay.setSample(v->getVisualSample());
            //envelopeDisplay.setADSR(v->getADSRParameters().attack,
            //    v->getADSRParameters().decay,
            //    v->getADSRParameters().sustain,
            //    v->getADSRParameters().release);
            //filterDisplay.updateFilter(v->getFilterCoefficients(), currentSampleRate);

            //auto params = v->getADSRParameters();
            //envelopeDisplay.setADSR(params.attack, params.decay, params.sustain, params.release);
            //filterDisplay.updateFilter(v->getFilterCoefficients(), currentSampleRate);

            //if (v->isNoteActive())
            //    envelopeDisplay.startEnvelopeVisual();
            //else
            //    envelopeDisplay.stopEnvelopeVisual();

            v->setOscType(params.oscType);
            v->setFilterCutoff(params.filterCutoff);
            v->setFilterResonance(params.filterResonance);

            v->setADSR(params.attack, params.decay, params.sustain, params.release);


            break;
        }
    }
}

void MainComponent::releaseResources() {}

void MainComponent::paint(juce::Graphics& g)
{
    g.fillAll(juce::Colours::darkgrey);
}

void MainComponent::resized()
{
    auto area = getLocalBounds().reduced(10);
    seedComponent.setBounds(area.removeFromTop(60));
    keyboardComponent.setBounds(area.removeFromBottom(100));

    auto visArea = area.reduced(10);
    oscDisplay.setBounds(visArea.removeFromTop(visArea.getHeight() / 3));
    filterDisplay.setBounds(visArea.removeFromTop(visArea.getHeight() / 2));
    envelopeDisplay.setBounds(visArea); // reste
}
