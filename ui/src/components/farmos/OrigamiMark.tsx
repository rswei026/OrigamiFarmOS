// The FarmOS brand mark: a folded paper corner ("dog-ear"), the same
// motif used on Card's `folded` treatment (Ch.13 design system) - every
// "sheet" in the product, including the logo itself, shares one
// origami-inspired visual language instead of a generic plant/leaf icon.
export function OrigamiMark({ className, size = 32 }: { className?: string; size?: number }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 64 64"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
      role="img"
      aria-label="Origami FarmOS"
    >
      <rect x="4" y="4" width="56" height="56" rx="16" fill="var(--color-primary, #e2603f)" />
      {/* folded corner shadow */}
      <path d="M40 4 L60 4 L60 24 Z" fill="var(--color-fold-dark, #c8452c)" opacity="0.35" />
      {/* folded corner flap */}
      <path d="M42 4 L60 4 L60 22 Z" fill="var(--color-fold-light, #f7c98e)" />
      {/* crease line */}
      <line x1="42" y1="4" x2="60" y2="22" stroke="var(--color-fold-dark, #c8452c)" strokeWidth="1.5" opacity="0.5" />
    </svg>
  )
}
