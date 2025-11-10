#pragma once
#include <JuceHeader.h> // indispensable pour juce:: types et int64

class SeedManager
{
public:
    SeedManager();

    void generateNewSeed();
    juce::int64 getSeed() const;
    juce::String getSeedString() const;

    std::function<void()> onSeedChanged;

private:
    juce::int64 seed; // type correct pour les entiers 64 bits
};


struct SynthParameters
{
    int oscType = 0;       // 0=sine, 1=saw, 2=square, 3=triangle
    float filterCutoff = 1000.0f; // Hz
    float filterResonance = 1.0f;
    float attack = 0.01f;
    float decay = 0.1f;
    float sustain = 0.8f;
    float release = 0.2f;
};

class SeedManager
{
public:
    SeedManager();
    void generateNewSeed();
    juce::int64 getSeed() const;
    juce::String getSeedString() const;

    std::function<void()> onSeedChanged;

    SynthParameters getMappedParameters() const;

private:
    juce::int64 seed;
};
