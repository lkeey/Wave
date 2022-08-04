class GradientAnimation{
    constructor() {
        this.cnv = document.querySelector('canvas');
        this.ctx = this.cnv.getContext('2d')

        this.circlesNum = 10;
        this.speed = 0.005;

        this.minRadius = 400;
        this.maxRadius = 800;

        this.setCanvasSize();
        this.createCircles();
        this.drawAnimation();

        window.onresize = () => {
            this.setCanvasSize();
            this.createCircles();
        }
    }
    setCanvasSize() {
        this.w = this.cnv.width = innerWidth;
        this.h = this.cnv.height = innerHeight;
    }

    createCircles() {
        this.cirlces = [];
        for (let i = 0 ; i < this.circlesNum ; ++i){
            this.cirlces.push( new Circle(this.w, this.h, this.minRadius, this.maxRadius) );
        }    
    }
    drawCircles() {
        this.cirlces.forEach(circle => circle.draw(this.ctx, this.speed));
    }

    clearCanvas() {
        this.ctx.clearRect(0,0, this.w, this.h);
    }

    drawAnimation() {
        this.clearCanvas();
        this.drawCircles();
        requestAnimationFrame( () => this.drawAnimation() );
    }
}

class Circle{
    constructor(w, h, minR, maxR) {
        this.x = Math.random() * w;
        this.y = Math.random() * h;

        this.angle = Math.random() * 2 * Math.PI;

        this.radius = Math.random() * (maxR-minR) + minR;

        this.firstColor = `hsla(${Math.random() * 360}, 75%, 50%, 1)`
        this.secondColor = `hsla(${Math.random() * 360}, 100%, 50%, 0)`
    }
    draw(ctx, speed) {
        this.angle += speed;

        const x = this.x + Math.cos(this.angle) * 200;
        const y = this.y + Math.sin(this.angle) * 200;
        const gradient = ctx.createRadialGradient(x, y, 0, x, y, this.radius);

                gradient.addColorStop(0, this.firstColor);
                gradient.addColorStop(1, this.secondColor);

        // ctx.globalCompositeOperation = `saturation`;
        ctx.globalCompositeOperation = `overlay`;

        ctx.fillStyle = gradient;
        ctx.beginPath()
        ctx.arc(x, y, this.radius, 0, 2*Math.PI);
        ctx.fill();
    }
}

window.onload = () => new GradientAnimation();