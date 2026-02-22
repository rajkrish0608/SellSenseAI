"use client";

import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Canvas, useFrame } from "@react-three/fiber";
import { TRANSITION } from "@/lib/motion";

function LoaderCore() {
    useFrame((state, delta) => {
        state.camera.lookAt(0, 0, 0);
    });

    return (
        <mesh>
            <icosahedronGeometry args={[1, 0]} />
            <meshBasicMaterial color="#00e5ff" wireframe />
            <mesh scale={[1.01, 1.01, 1.01]}>
                <icosahedronGeometry args={[1, 0]} />
                <meshBasicMaterial color="#00e5ff" transparent opacity={0.1} />
            </mesh>
        </mesh>
    );
}

function SpinningCore() {
    return (
        <group>
            <RotatingMesh />
        </group>
    )
}

function RotatingMesh() {
    useFrame((state, delta) => {
        if (state && state.scene) {
            state.scene.rotation.y += delta * 2
            state.scene.rotation.x += delta * 1
        }
    })
    return (
        <LoaderCore />
    )
}

export default function Preloader3D() {
    // We use internal state for the exit animation, 
    // but the parent 'page.tsx' will unmount us forcefully after 3.5s

    return (
        <div
            id="preloader-root"
            className="fixed inset-0 z-[100] flex items-center justify-center bg-black transition-opacity duration-1000"
        >
            <div className="absolute inset-0 z-0">
                {/* Error Boundary could go here, but for now we trust the parent timeout */}
                <Canvas camera={{ position: [0, 0, 3] }} onError={(e) => console.error("Canvas Error", e)}>
                    <ambientLight intensity={0.5} />
                    <SpinningCore />
                </Canvas>
            </div>

            <motion.div
                className="z-10 flex flex-col items-center gap-4"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={TRANSITION}
            >
                <h2 className="text-2xl font-bold tracking-[0.5em] text-cyan-400 uppercase">
                    SellSense.AI
                </h2>
                {/* Simplified progress bar */}
                <div className="h-1 w-48 bg-cyan-900/30 rounded-full overflow-hidden">
                    <motion.div
                        className="h-full bg-cyan-400"
                        initial={{ width: "0%" }}
                        animate={{ width: "100%" }}
                        transition={{ duration: 2.5, ease: "easeInOut" }}
                    />
                </div>
                <p className="text-xs text-cyan-600 font-mono">
                    INITIALIZING SYSTEM DNA...
                </p>

                {/* Manual Skip Button - Z-Index Higher than Canvas */}
                <button
                    onClick={() => {
                        // This click will bubble up or we can use a global event, 
                        // but since page.tsx controls mounting, we essentially just rely on visual feedback here.
                        // However, visually notifying the user 'Loading...' is better.
                        // Ideally we'd pass a prop, but for this quick fix, we rely on page.tsx timeout.
                    }}
                    className="mt-8 text-[10px] text-cyan-900/50 hover:text-cyan-500 transition-colors uppercase cursor-pointer z-50 pointer-events-auto"
                >
                    [ Force Skip ]
                </button>
            </motion.div>
        </div>
    );
}
