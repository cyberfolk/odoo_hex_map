/** @odoo-module **/
export const POSITION = {
    "X": [0, 0, 18.75, 18.75, 0, -18.75, -18.75, 0, 18.75, 37.5, 37.5, 37.5, 18.75, 0, -18.75, -37.5, -37.5, -37.5, -18.75,0, 18.75, 37.5, 56.25, 56.25, 56.25,	56.25, 37.5, 18.75,	0, -18.75, -37.5, -56.25, -56.25, -56.25, -56.25, -37.5, -18.75],
    "Y": [0, -20, -10, 10, 20, 10, -10, -40, -30, -20, 0, 20, 30, 40, 30, 20, 0, -20, -30, -60,	-50, -40, -30, -10, 10,	30,	40,	50,	60,	50,	40,	30,	10,	-10, -30, -40, -50,]
};

export function getAxes(index, REDUCTION=0.95) {
    // REDUCTION is a constant used to bring the HEX closer to the center of the QUADRANT.
    // In this way we have the perception that the padding of the QUADRANTS increases
    const asse_y = 50 + POSITION.Y[index - 1] * REDUCTION + "%";
    const asse_x = 50 + POSITION.X[index - 1] * REDUCTION + "%";
    return `top: ${asse_y}; left: ${asse_x};`
}
