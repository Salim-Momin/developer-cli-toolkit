"use client";

import { motion } from "framer-motion";


const particles = Array.from({ length: 18 }, (_, i) => i);


export default function FeatureParticles() {

  return (
    <div
      className="
      pointer-events-none
      absolute
      inset-0
      overflow-hidden
      "
    >

      {particles.map((p) => (

        <motion.span
          key={p}

          initial={{
            opacity: 0,
            y: "100vh",
            x: `${Math.random() * 100}vw`,
          }}

          animate={{
            opacity: [0, 0.8, 0],
            y: "-20vh",
          }}

          transition={{
            duration: 8 + Math.random() * 8,
            repeat: Infinity,
            delay: Math.random() * 5,
            ease: "linear",
          }}

          className="
          absolute
          h-1
          w-1
          rounded-full
          bg-cyan-400
          shadow-[0_0_12px_#22d3ee]
          "
        />

      ))}

    </div>
  );
}