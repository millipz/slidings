<script>
  import { onMount } from 'svelte';

  let gameId = null;
  let gameState = null;
  let result = null;

  const startGame = async () => {
    const response = await fetch('http://localhost:8000/start', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    const data = await response.json();
    gameId = data.game_id;
    gameState = data.game_state;
  };

  const hit = async () => {
    const response = await fetch('http://localhost:8000/hit', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ game_id: gameId }),
    });
    const data = await response.json();
    result = data.result;
    gameState = data.game_state;
  };

  const stick = async () => {
    const response = await fetch('http://localhost:8000/stick', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ game_id: gameId }),
    });
    const data = await response.json();
    result = data.result;
    gameState = data.game_state;
  };

  onMount(() => {
    startGame();
  });
</script>

<main>
  <h1>Pontoon Game</h1>

  {#if !gameId}
    <p>Loading...</p>
  {:else}
    <div>
      <h2>Hand</h2>
      <pre>{JSON.stringify(gameState["player_hand"])}</pre>
    </div>

    <div>
      <h2>Result</h2>
      <p>{JSON.stringify(result)}</p>
    </div>

    <div>
      <button on:click={startGame}>New Game</button>
      <button on:click={hit}>Hit</button>
      <button on:click={stick}>Stick</button>
    </div>
  {/if}
</main>

<style>
  main {
    max-width: 800px;
    margin: 0 auto;
    padding: 1rem;
  }

  pre {
    white-space: pre-wrap;
  }
</style>