"use client";

import { useState } from "react";
import {
  motion,
  useMotionValue,
  useSpring,
  useTransform,
} from "framer-motion";

import { Check, Copy, Terminal } from "lucide-react";

type Props = {
  title: string;
  command: string;
};

export default function InstallCard({
  title,
  command,
}: Props) {
  const [copied, setCopied] = useState(false);

  const x = useMotionValue(0);
  const y = useMotionValue(0);

  const rotateX = useSpring(useTransform(y, [-0.5, 0.5], [10, -10]), {
    stiffness: 220,
    damping: 18,
  });

  const rotateY = useSpring(useTransform(x, [-0.5, 0.5], [-10, 10]), {
    stiffness: 220,
    damping: 18,
  });

  function handleMove(
    e: React.MouseEvent<HTMLDivElement>
  ) {
    const rect = e.currentTarget.getBoundingClientRect();

    x.set((e.clientX - rect.left) / rect.width - 0.5);
    y.set((e.clientY - rect.top) / rect.height - 0.5);
  }

  function leave() {
    x.set(0);
    y.set(0);
  }

  async function copyCommand() {
    await navigator.clipboard.writeText(command);

    setCopied(true);

    setTimeout(() => {
      setCopied(false);
    }, 1800);
  }

  return (
    <motion.div
      onMouseMove={handleMove}
      onMouseLeave={leave}
      style={{
        rotateX,
        rotateY,
        transformPerspective: 1400,
      }}
      whileHover={{
        y: -10,
        scale: 1.02,
      }}
      className="group relative overflow-hidden rounded-3xl border border-cyan-500/20 bg-white/[0.02] backdrop-blur-xl"
    >
      {/* Glow */}

      <div className="absolute inset-0 opacity-0 transition duration-500 group-hover:opacity-100">
        <div className="absolute inset-0 bg-cyan-500/5" />

        <div className="absolute left-1/2 top-1/2 h-72 w-72 -translate-x-1/2 -translate-y-1/2 rounded-full bg-cyan-500/15 blur-[120px]" />
      </div>

      {/* Animated Border */}

      <motion.div
        animate={{
          rotate: 360,
        }}
        transition={{
          repeat: Infinity,
          duration: 12,
          ease: "linear",
        }}
        className="absolute inset-[-150%] bg-conic-from-90 from-transparent via-cyan-500/40 to-transparent"
      />

      <div className="absolute inset-[1px] rounded-3xl bg-[#070707]" />

      {/* Reflection */}

      <motion.div
        animate={{
          x: ["-120%", "220%"],
        }}
        transition={{
          repeat: Infinity,
          duration: 5,
          ease: "linear",
        }}
        className="absolute top-0 left-0 h-full w-1/3 skew-x-[-20deg] bg-gradient-to-r from-transparent via-white/10 to-transparent"
      />

      <div className="relative z-20 p-4 sm:p8">
        {/* Header */}

        <div className="mb-8 flex items-center justify-between gap-3">
          <div className="flex items-center gap-3">
            <div className="rounded-lg bg-cyan-500/10 p-3">
              <Terminal
                className="text-cyan-400"
                size={20}
              />
            </div>

            <div>
              <p className="text-sm text-zinc-500">
                {title}
              </p>

              <h3 className="font-semibold text-white">
                Installation
              </h3>
            </div>
          </div>

          <motion.button
            whileTap={{
              scale: 0.9,
            }}
            whileHover={{
              scale: 1.05,
            }}
            onClick={copyCommand}
            className="rounded-xl border border-cyan-500/20 bg-cyan-500/10 p-3 transition hover:bg-cyan-500/20"
          >
            {copied ? (
              <Check
                className="text-green-400"
                size={18}
              />
            ) : (
              <Copy
                className="text-cyan-400"
                size={18}
              />
            )}
          </motion.button>
        </div>

        {/* Command */}

            {/* Command */}

<motion.div
  whileHover={{
    scale: 1.01,
  }}
  className="
  rounded-xl
  border
  border-cyan-500/10
  bg-black/50
  p-4
  sm:p-5
  overflow-hidden
  "
>

<pre
className="
whitespace-pre-wrap
break-words
overflow-x-auto
font-mono
text-xs
sm:text-sm
leading-relaxed
text-cyan-300
"
>

<span className="text-cyan-500">
$
</span>{" "}

{command}

</pre>


</motion.div>

        {/* Footer */}

        <div className="mt-6 flex items-center justify-between text-xs text-zinc-500">
          <span>Ready to use</span>

          <span className="text-cyan-400">
            DevKit v0.1.5
          </span>
        </div>
      </div>
    </motion.div>
  );
}