// Utility to load words from words.txt file
let cachedWords: string[] | null = null;

export async function loadWords(): Promise<string[]> {
  if (cachedWords) {
    return cachedWords;
  }

  try {
    const response = await fetch('/words.txt');
    const text = await response.text();
    cachedWords = text
      .split('\n')
      .map(word => word.trim().toUpperCase())
      .filter(word => word.length === 5); // Only 5-letter words
    return cachedWords;
  } catch (error) {
    console.error('Failed to load words.txt:', error);
    // Fallback to empty array or default words
    return [];
  }
}

export function getRandomWordFromList(words: string[]): string {
  if (words.length === 0) {
    throw new Error('Word list is empty');
  }
  const index = Math.floor(Math.random() * words.length);
  return words[index];
}

export function getDailyWordFromList(words: string[], date: Date): string {
  if (words.length === 0) {
    throw new Error('Word list is empty');
  }
  
  const epoch = Date.UTC(2021, 5, 19);
  const dayMs = 24 * 60 * 60 * 1000;
  const today = Date.UTC(
    date.getUTCFullYear(),
    date.getUTCMonth(),
    date.getUTCDate()
  );
  const day = Math.floor((today - epoch) / dayMs);
  const index = ((day % words.length) + words.length) % words.length;
  
  return words[index];
}
