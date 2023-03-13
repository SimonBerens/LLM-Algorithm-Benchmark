export function objectEntries<K extends string, V>(o: Record<K, V>): [K, V][] {
    return Object.entries(o) as [K, V][]
}

export function objectFromEntries<K extends string, V>(o: [K, V][]): Record<K, V> {
    return Object.fromEntries(o) as Record<K, V>
}