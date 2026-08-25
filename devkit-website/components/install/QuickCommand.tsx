"use client";

import { useState } from "react";

import {
  motion,
  useMotionValue,
  useSpring,
  useTransform,
} from "framer-motion";

import {
  Check,
  Copy,
  Terminal,
} from "lucide-react";

type Props = {
  title: string;
  command: string;
};

export default function QuickCommand({
  title,
  command,
}: Props) {
  const [copied, setCopied] = useState(false);

  const mouseX = useMotionValue(0);
  const mouseY = useMotionValue(0);

  const rotateX = useSpring(
    useTransform(mouseY, [-0.5, 0.5], [8, -8])
  );

  const rotateY = useSpring(
    useTransform(mouseX, [-0.5, 0.5], [-8, 8])
  );

  function handleMove(
    e: React.MouseEvent<HTMLDivElement>
  ) {
    const rect = e.currentTarget.getBoundingClientRect();

    mouseX.set(
      (e.clientX - rect.left) / rect.width - 0.5
    );

    mouseY.set(
      (e.clientY - rect.top) / rect.height - 0.5
    );
  }

  function reset() {
    mouseX.set(0);
    mouseY.set(0);
  }

  async function copy() {
    await navigator.clipboard.writeText(command);

    setCopied(true);

    setTimeout(() => {
      setCopied(false);
    }, 1500);
  }

  return (
    <motion.div
      onMouseMove={handleMove}
      onMouseLeave={reset}
      whileHover={{
        y: -10,
        scale: 1.03,
      }}
      style={{
        rotateX,
        rotateY,
        transformPerspective: 1200,
      }}
      className="group relative overflow-hidden rounded-2xl border border-cyan-500/10 bg-zinc-950/60 backdrop-blur-xl"
    >
      <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/5 via-transparent to-transparent opacity-0 transition duration-500 group-hover:opacity-100" />

      <div className="relative p-6">
        <div className="mb-5 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Terminal
              className="text-cyan-400"
              size={18}
            />

            <span className="font-semibold text-white">
              {title}
            </span>
          </div>

          <button
            onClick={copy}
            className="rounded-lg p-2 transition hover:bg-cyan-500/10"
          >
            {copied ? (
              <Check
                size={16}
                className="text-green-400"
              />
            ) : (
              <Copy
                size={16}
                className="text-cyan-400"
              />
            )}
          </button>
        </div>

        <div className="rounded-xl border border-cyan-500/10 bg-black/70 p-4 font-mono text-sm text-cyan-300">
          <span className="text-cyan-500">$ </span>

          {command}

          <motion.span
            animate={{
              opacity: [0, 1, 0],
            }}
            transition={{
              repeat: Infinity,
              duration: 1,
            }}
            className="ml-1"
          >
            █
          </motion.span>
        </div>
      </div>
    </motion.div>
  );
}