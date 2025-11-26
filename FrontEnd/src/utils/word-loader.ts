// Utility to load words from backend API
import { solverAPI } from './api-utils';

let cachedWords: string[] = [];
let loadingPromise: Promise<string[]> | null = null;

export async function loadWords(): Promise<string[]> {
  if (cachedWords.length > 0) {
    return cachedWords;
  }

  // If already loading, return the same promise
  if (loadingPromise) {
    return loadingPromise;
  }

  loadingPromise = (async () => {
    try {
      // Try to load from backend first
      const isBackendHealthy = await solverAPI.healthCheck();
      
      if (isBackendHealthy) {
        console.log('📚 Loading word list from backend...');
        cachedWords = await solverAPI.getAllWords();
        console.log(`✅ Loaded ${cachedWords.length} words from backend`);
        return cachedWords;
      }
      
      // Fallback: load from local file if backend fails
      console.log('⚠️ Backend not available, trying local words.txt...');
      const response = await fetch('/words.txt');
      if (response.ok) {
        const text = await response.text();
        cachedWords = text
          .split('\n')
          .map(word => word.trim().toUpperCase())
          .filter(word => word.length === 5);
        console.log(`✅ Loaded ${cachedWords.length} words from local file`);
        return cachedWords;
      }
      
      throw new Error('Both backend and local file failed');
    } catch (error) {
      console.error('❌ Failed to load words:', error);
      // Return empty array as last resort
      return [];
    } finally {
      loadingPromise = null;
    }
  })();

  return loadingPromise;
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
