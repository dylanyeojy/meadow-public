import { Pressable, PressableProps, StyleProp, ViewStyle } from "react-native";
import Animated, {
    Easing,
    useAnimatedStyle,
    useReducedMotion,
    useSharedValue,
    withTiming,
} from "react-native-reanimated";

const AnimatedPressable = Animated.createAnimatedComponent(Pressable);
const timing = { duration: 140, easing: Easing.bezier(0.23, 1, 0.32, 1) };

type Props = Omit<PressableProps, "style"> & { style?: StyleProp<ViewStyle> };

export function PressableScale({ style, children, ...rest }: Props) {
    const scale = useSharedValue(1);
    const reduceMotion = useReducedMotion();
    const animatedStyle = useAnimatedStyle(() => ({
        transform: [{ scale: scale.value }],
    }));

    return (
        <AnimatedPressable
            {...rest}
            onPressIn={() => {
                if (reduceMotion) return;
                scale.value = withTiming(0.97, timing);
            }}
            onPressOut={() => {
                scale.value = withTiming(1, timing);
            }}
            style={[style, animatedStyle]}
        >
            {children}
        </AnimatedPressable>
    );
}
