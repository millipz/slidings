<script>
  import { onMount } from "svelte";

  let gameId = null;
  let gameState = null;
  let result = null;
  let svgPaths = null;
  let cardIcons = null;

  function loadSvgPaths() {
    fetch("/assets/icon_paths.json")
      .then((response) => {
        if (!response.ok) {
          throw new Error("HTTP error " + response.status);
        }
        return response.json();
      })
      .then((json) => {
        svgPaths = json;
      })
      .catch((error) => {
        console.error("Error fetching SVG paths:", error);
      });
  }

  const createIcon = (rank, suit) => {
    let colour;
    if (suit === "diamonds" || suit === "hearts") {
      colour = "#000000";
    } else {
      colour = "#ff0000";
    }

    const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("xmlns", "http://www.w3.org/2000/svg");
    svg.setAttribute("viewBox", "0 -0.5 9 9");
    svg.setAttribute("shape-rendering", "crispEdges");

    const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
    path.setAttribute("stroke", colour);
    path.setAttribute("d", svgPaths[rank]);

    svg.appendChild(path);

    return svg;
  };

  const generateCardIcons = async () => {
    await loadSvgPaths();

    const output = {};

    for (const suit of ["clubs", "diamonds", "hearts", "spades"]) {
      for (const rank of [...Array(14).keys()]) {
        const svgIcon = createIcon(rank, suit);
        output[rank + suit] = svgIcon;
      }
    }

    const svgIcon = createIcon("back", "back");
    output["back"] = svgIcon;

    cardIcons = output;
    $: console.log("cardIcons updated:", cardIcons);
  };

  const startGame = async () => {
    const response = await fetch("http://localhost:8000/start", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });
    const data = await response.json();
    gameId = data.game_id;
    gameState = data.game_state;
  };

  const hit = async () => {
    const response = await fetch("http://localhost:8000/hit", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ game_id: gameId }),
    });
    const data = await response.json();
    result = data.result;
    gameState = data.game_state;
  };

  const stick = async () => {
    const response = await fetch("http://localhost:8000/stick", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ game_id: gameId }),
    });
    const data = await response.json();
    result = data.result;
    gameState = data.game_state;
  };

  onMount(() => {
    startGame();
    loadSvgPaths();
    generateCardIcons();
  });
</script>

<main>
  <h1>Pontoon Game</h1>

  {#await generateCardIcons()}
    <p>Loading...</p>
  {:then cardIcons}
    {#if !gameId}
      <p>Starting Game...</p>
    {:else}
      <div>
        <h2>Dealer's Hand</h2>
        <div class="cards">

        </div>
      </div>

      <div>
        <h2>Player's Hand</h2>
        <div class="cards">

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
  {/await}
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
