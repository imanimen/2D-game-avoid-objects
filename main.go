package main

import (
	"image/color"
	"log"
	"math/rand"
	"time"

	"github.com/hajimehoshi/ebiten/v2"
)

const (
	screenWidth  = 600
	screenHeight = 400
	playerWidth  = 50
	playerHeight = 50
	obstacleWidth = 20
	obstacleHeight = 20
)

type Game struct {
	playerX float64
	playerY float64
	obstacles []Obstacle
	score int
}

type Obstacle struct {
	x float64
	y float64
}

func (g *Game) Update() error {
	// Move the player
	if ebiten.IsKeyPressed(ebiten.KeyLeft) && g.playerX > 0 {
		g.playerX -= 5
	}
	if ebiten.IsKeyPressed(ebiten.KeyRight) && g.playerX < screenWidth - playerWidth {
		g.playerX += 5
	}

	// Move the obstacles
	for i := range g.obstacles {
		g.obstacles[i].y += 3
		if g.obstacles[i].y > screenHeight {
			// Remove the obstacle if it goes off-screen
			g.obstacles = append(g.obstacles[:i], g.obstacles[i+1:]...)
			g.score++
		}
	}

	// Add a new obstacle randomly
	if rand.Intn(100) < 10 {
		g.obstacles = append(g.obstacles, Obstacle{x: rand.Float64() * (screenWidth - obstacleWidth), y: 0})
	}

	// Check for collisions
	for _, obs := range g.obstacles {
		if g.playerX < obs.x + obstacleWidth && g.playerX + playerWidth > obs.x && g.playerY < obs.y + obstacleHeight && g.playerY + playerHeight > obs.y {
			return nil
		}
	}

	return nil
}

func (g *Game) Draw(screen *ebiten.Image) {
	// Draw the player
	ebitenutil.DrawRect(screen, g.playerX, g.playerY, playerWidth, playerHeight, color.White)

	// Draw the obstacles
	for _, obs := range g.obstacles {
		ebitenutil.DrawRect(screen, obs.x, obs.y, obstacleWidth, obstacleHeight, color.Red)
	}

	// Draw the score
	ebitenutil.DebugPrint(screen, fmt.Sprintf("Score: %d", g.score))
}

func (g *Game) Layout(outsideWidth, outsideHeight int) (screenWidth, screenHeight int) {
	return screenWidth, screenHeight
}

func main() {
	rand.Seed(time.Now().UnixNano())

	ebiten.SetWindowSize(screenWidth, screenHeight)
	ebiten.SetWindowTitle("Dodge the Obstacles")
	if err := ebiten.RunGame(&Game{playerX: screenWidth / 2, playerY: screenHeight - playerHeight}); err != nil {
		log.Fatal(err)
	}
}
