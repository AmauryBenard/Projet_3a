#include "SeedManager.h"

SeedManager::SeedManager()
{
    generateNewSeed();
}

void SeedManager::generateNewSeed()
{
    seed = juce::Random::getSystemRandom().nextInt64();

    if (onSeedChanged)
        onSeedChanged();
}

juce::int64 SeedManager::getSeed() const
{
    return seed;
}

juce::String SeedManager::getSeedString() const
{
    return juce::String(seed);
}



SeedManager::SynthParameters SeedManager::getMappedParameters() const
{
    SynthParameters params;
    auto seedStr = getSeedString();

    // Pour chaque chiffre, on mappe sur un parame
    if (seedStr.length() >= 7)
    {
        params.oscType = seedStr[0] % 4; // 0-3
        params.filterCutoff = 200.0f + (seedStr[1] - '0') * 1000.0f; // exemple
        params.filterResonance = 0.5f + (seedStr[2] - '0') * 0.5f;
        params.attack = 0.01f + (seedStr[3] - '0') * 0.05f;
        params.decay = 0.05f + (seedStr[4] - '0') * 0.05f;
        params.sustain = 0.5f + (seedStr[5] - '0') * 0.05f;
        params.release = 0.1f + (seedStr[6] - '0') * 0.1f;
    }

    return params;
}
