import { Pressable, StyleSheet } from "react-native";
import Animated, {
    Easing,
    useAnimatedStyle,
    useReducedMotion,
    withTiming,
} from "react-native-reanimated";
import { colors } from "@/theme";

type Props = {
    value: boolean;
    onChange: (next: boolean) => void;
};

export function Toggle({ value, onChange }: Props) {
    const reduceMotion = useReducedMotion();
    const animatedKnob = useAnimatedStyle(() => ({
        transform: [
            {
                translateX: withTiming(value ? 21 : 0, {
                    duration: reduceMotion ? 0 : 160,
                    easing: Easing.bezier(0.23, 1, 0.32, 1),
                }),
            },
        ],
    }));

    return (
        <Pressable
            onPress={() => onChange(!value)}
            hitSlop={{ top: 7, bottom: 7 }}
            accessibilityRole="switch"
            accessibilityState={{ checked: value }}
            style={[styles.track, value && styles.trackOn]}
        >
            <Animated.View style={[styles.knob, animatedKnob]} />
        </Pressable>
    );
}

const styles = StyleSheet.create({
    track: {
        width: 52,
        height: 31,
        borderRadius: 999,
        backgroundColor: colors.faint,
    },
    trackOn: {
        backgroundColor: colors.sage,
    },
    knob: {
        position: "absolute",
        top: 2,
        left: 2,
        width: 27,
        height: 27,
        borderRadius: 999,
        backgroundColor: colors.surface,
    },
});
