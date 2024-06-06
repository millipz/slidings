<script>
  import { onMount } from 'svelte';

  let gameId = null;
  let gameState = null;
  let result = null;

  const getRankIcon = (rank) => {
    return "assets/" + rank.toString() + ".png";
  };

  const getSuitIcon = (suit) => {
    const suitNames = {
      1: "clubs",
      2: "diamonds",
      3: "hearts",
      4: "spades"
    }
    let suitName = suitNames[suit]
    return "assets/" + suitName + ".png";
  };

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
    <h2>Dealer's Hand</h2>
    <div class="cards">
      {#each gameState.dealer_hand as card}
      {#if card === "Hidden" && !gameState.game_over}
      <img src="assets/card_back.png" alt="Card Back" />
      {:else}
      <img src={getRankIcon(card.rank)} alt="Card" />
      <img src={getSuitIcon(card.suit)} alt="Card" />
      {/if}
      {/each}
    </div>
  </div>

  <div>
    <h2>Player's Hand</h2>
    <div class="cards">
      {#each gameState.player_hand as card}
        <img src={getRankIcon(card.rank)} alt="Card" />
        <img src={getSuitIcon(card.suit)} alt="Card" />
      {/each}
    </div>
  </div>

    <div>
      <h2>Result</h2>
      <p>{result ? JSON.stringify(result.message) : "No result yet"}</p>
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

  .cards {
    display: flex;
    gap: 0.5rem;
  }

  .cards img {
    width: 100px;
    height: 150px;
    object-fit: contain;
    image-rendering: pixelated;
    image-rendering: -moz-crisp-edges;
    image-rendering: crisp-edges;
  }

  pre {
    white-space: pre-wrap;
  }
</style>
