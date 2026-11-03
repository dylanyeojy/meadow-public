import Svg, { Circle, Path, Rect } from "react-native-svg";

export function HomeIcon({ color }: { color: string }) {
    return (
        <Svg
            viewBox="0 0 24 24"
            fill="none"
            stroke={color}
            strokeWidth={1.9}
            strokeLinecap="round"
            strokeLinejoin="round"
            width={24}
            height={24}
        >
            <Path d="M3 10.5 12 3l9 7.5" />
            <Path d="M5 9.5V20h5v-6h4v6h5V9.5" />
        </Svg>
    );
}

export function CalendarIcon({ color }: { color: string }) {
    return (
        <Svg
            viewBox="0 0 24 24"
            fill="none"
            stroke={color}
            strokeWidth={1.9}
            strokeLinecap="round"
            strokeLinejoin="round"
            width={24}
            height={24}
        >
            <Rect x={3.5} y={4.5} width={17} height={16} rx={3.5} />
            <Path d="M3.5 9h17M8 3v3M16 3v3" />
        </Svg>
    );
}

export function StatsIcon({ color }: { color: string }) {
    return (
        <Svg
            viewBox="0 0 24 24"
            fill="none"
            stroke={color}
            strokeWidth={1.9}
            strokeLinecap="round"
            strokeLinejoin="round"
            width={24}
            height={24}
        >
            <Path d="M5 19V11M12 19V5M19 19v-6" />
        </Svg>
    );
}

export function MoreIcon({ color }: { color: string }) {
    return (
        <Svg viewBox="0 0 24 24" fill={color} width={24} height={24}>
            <Circle cx={5} cy={12} r={1.4} />
            <Circle cx={12} cy={12} r={1.4} />
            <Circle cx={19} cy={12} r={1.4} />
        </Svg>
    );
}

export function PlusIcon({
    color,
    size = 24,
}: {
    color: string;
    size?: number;
}) {
    return (
        <Svg
            viewBox="0 0 24 24"
            fill="none"
            stroke={color}
            strokeWidth={2.4}
            strokeLinecap="round"
            strokeLinejoin="round"
            width={size}
            height={size}
        >
            <Path d="M12 5v14M5 12h14" />
        </Svg>
    );
}

export function SproutIcon({
    color,
    size = 32,
}: {
    color: string;
    size?: number;
}) {
    return (
        <Svg
            viewBox="0 0 24 24"
            fill="none"
            stroke={color}
            strokeWidth={2.2}
            strokeLinecap="round"
            strokeLinejoin="round"
            width={size}
            height={size}
        >
            <Path d="M12 21V10" />
            <Path d="M12 21c0-3.5 1.4-6.4 4.5-8.4" />
            <Path d="M12 21c0-3.5-1.4-6.4-4.5-8.4" />
            <Path d="M12 21c1-2.4 3-3.8 6-4.4" />
            <Path d="M12 21c-1-2.4-3-3.8-6-4.4" />
        </Svg>
    );
}

export function EyeOffIcon({
    color,
    size,
    strokeWidth = 2,
}: {
    color: string;
    size: number;
    strokeWidth?: number;
}) {
    return (
        <Svg
            viewBox="0 0 24 24"
            stroke={color}
            width={size}
            height={size}
            strokeWidth={strokeWidth}
            fill="none"
            strokeLinecap="round"
            strokeLinejoin="round"
        >
            <Path d="M17.94 17.94A10.1 10.1 0 0 1 12 19.5C5 19.5 1.5 12 1.5 12a18.5 18.5 0 0 1 5.06-5.94M9.9 4.74A9.5 9.5 0 0 1 12 4.5c7 0 10.5 7.5 10.5 7.5a18.4 18.4 0 0 1-2.16 3.19" />
            <Path d="M9.88 9.88a3.2 3.2 0 0 0 4.24 4.24" />
            <Path d="M2 2l20 20" />
        </Svg>
    );
}

export function EyeOnIcon({
    color,
    size,
    strokeWidth = 2,
}: {
    color: string;
    size: number;
    strokeWidth?: number;
}) {
    return (
        <Svg
            viewBox="0 0 24 24"
            stroke={color}
            width={size}
            height={size}
            strokeWidth={strokeWidth}
            fill="none"
            strokeLinecap="round"
            strokeLinejoin="round"
        >
            <Path d="M1.5 12S5 4.5 12 4.5 22.5 12 22.5 12 19 19.5 12 19.5 1.5 12 1.5 12z" />
            <Circle cx="12" cy="12" r="3" />
        </Svg>
    );
}

export function CheckIcon({
    color,
    size,
    strokeWidth = 3,
}: {
    color: string;
    size: number;
    strokeWidth?: number;
}) {
    return (
        <Svg
            viewBox="0 0 24 24"
            fill="none"
            stroke={color}
            width={size}
            height={size}
            strokeWidth={strokeWidth}
            strokeLinecap="round"
            strokeLinejoin="round"
        >
            <Path d="M5 12l5 5L20 6" />
        </Svg>
    );
}

export function ClockIcon({
    color,
    size,
    strokeWidth = 2,
}: {
    color: string;
    size: number;
    strokeWidth?: number;
}) {
    return (
        <Svg
            viewBox="0 0 24 24"
            fill="none"
            stroke={color}
            width={size}
            height={size}
            strokeWidth={strokeWidth}
            strokeLinecap="round"
            strokeLinejoin="round"
        >
            <Circle cx="12" cy="12" r="9" />
            <Path d="M12 7.5V12l3 2" />
        </Svg>
    );
}

export function PencilIcon({
    color,
    size,
    strokeWidth = 2,
}: {
    color: string;
    size: number;
    strokeWidth?: number;
}) {
    return (
        <Svg
            viewBox="0 0 24 24"
            fill="none"
            stroke={color}
            width={size}
            height={size}
            strokeWidth={strokeWidth}
            strokeLinecap="round"
            strokeLinejoin="round"
        >
            <Path d="M12 20h9"></Path>
            <Path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"></Path>
        </Svg>
    );
}

export function TrashIcon({
    color,
    size,
    strokeWidth = 2,
}: {
    color: string;
    size: number;
    strokeWidth?: number;
}) {
    return (
        <Svg
            viewBox="0 0 24 24"
            fill="none"
            stroke={color}
            width={size}
            height={size}
            strokeWidth={strokeWidth}
            strokeLinecap="round"
            strokeLinejoin="round"
        >
            <Path d="M3 6h18M8 6V4h8v2M6 6l1 14h10l1-14"></Path>
            <Path d="M10 11v6M14 11v6"></Path>
        </Svg>
    );
}
