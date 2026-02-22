export const TRANSITION = {
    duration: 0.8,
    ease: [0.22, 1, 0.36, 1], // Custom "Power4.out" style easing
};

export const STAGGER = {
    container: {
        hidden: { opacity: 0 },
        show: {
            opacity: 1,
            transition: {
                staggerChildren: 0.1,
                delayChildren: 0.2,
            },
        },
    },
    item: {
        hidden: { opacity: 0, y: 20 },
        show: { opacity: 1, y: 0, transition: TRANSITION },
    },
    reveal: {
        hidden: { y: "100%" },
        show: { y: "0%", transition: { ...TRANSITION, duration: 1.2 } },
    },
};

export const HOVER = {
    scale: 1.05,
    glow: {
        boxShadow: "0 0 20px rgba(0, 229, 255, 0.4)",
        borderColor: "rgba(0, 229, 255, 0.6)",
    },
};
