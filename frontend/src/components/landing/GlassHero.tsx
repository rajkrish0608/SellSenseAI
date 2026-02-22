"use client";

import { useRef } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { Float, MeshTransmissionMaterial, Text, useGLTF } from "@react-three/drei";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import MagneticButton from "@/components/ui/MagneticButton";

function HolographicCard() {
    const mesh = useRef<any>(null);

    useFrame((state) => {
        if (!mesh.current) return;
        const t = state.clock.getElapsedTime();
        mesh.current.rotation.x = Math.sin(t / 4) * 0.1;
        mesh.current.rotation.y = Math.sin(t / 2) * 0.1;
        mesh.current.position.y = Math.sin(t / 1.5) * 0.1;
    });

    return (
        <group>
            <Float floatIntensity={2} rotationIntensity={1}>
                <mesh ref={mesh}>
                    <boxGeometry args={[3.5, 2, 0.2]} />
                    <MeshTransmissionMaterial
                        backside
                        backsideThickness={1.5}
                        thickness={0.5}
                        chromaticAberration={0.05}
                        anisotropy={0.5}
                        distortion={0.5}
                        distortionScale={0.5}
                        temporalDistortion={0.2}
                        color="#00e5ff"
                        background={undefined}
                    />
                </mesh>

                <Text
                    position={[0, 0, 0.15]}
                    fontSize={0.2}
                    color="white"
                    anchorX="center"
                    anchorY="middle"
                    font="/fonts/Inter-Bold.ttf"
                >
                    SELLSENSE.AI
                </Text>
            </Float>
        </group>
    );
}

export default function GlassHero() {
    return (
        <section className="relative h-screen w-full bg-black overflow-hidden flex flex-col items-center justify-center">
            {/* Background Gradients */}
            <div className="absolute top-[-20%] left-[-10%] w-[60vw] h-[60vw] bg-purple-900/20 rounded-full blur-[120px] pointer-events-none" />
            <div className="absolute bottom-[-20%] right-[-10%] w-[60vw] h-[60vw] bg-cyan-900/20 rounded-full blur-[120px] pointer-events-none" />

            <div className="z-10 text-center mb-8 pointer-events-none">
                <motion.h1
                    initial={{ opacity: 0, y: 50 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 1, ease: [0.22, 1, 0.36, 1] }}
                    className="text-6xl md:text-8xl font-bold tracking-tighter text-white mb-6"
                >
                    Future of <br />
                    <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-purple-500">
                        Marketing Logic
                    </span>
                </motion.h1>

                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.5, duration: 1 }}
                    className="flex gap-4 justify-center pointer-events-auto"
                >
                    <MagneticButton>
                        <Button size="lg" className="bg-white text-black hover:bg-cyan-50 rounded-full px-8 h-12 text-lg">
                            Start Platform
                        </Button>
                    </MagneticButton>
                    <MagneticButton>
                        <Button size="lg" variant="outline" className="text-white border-white/20 hover:bg-white/10 rounded-full px-8 h-12 text-lg">
                            View Demo
                        </Button>
                    </MagneticButton>
                </motion.div>
            </div>

            {/* 3D Scene */}
            <div className="absolute inset-0 z-0 opacity-60">
                <Canvas camera={{ position: [0, 0, 5], fov: 45 }}>
                    <ambientLight intensity={0.5} />
                    <spotLight position={[10, 10, 10]} angle={0.15} penumbra={1} />
                    <pointLight position={[-10, -10, -10]} />
                    <HolographicCard />
                </Canvas>
            </div>
        </section>
    );
}
