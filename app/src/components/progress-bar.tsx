import { StyleProp, ViewStyle, View, StyleSheet } from "react-native";
import { colors } from "@/theme";

type Props = {
    step: number;
    style?: StyleProp<ViewStyle>;
};

export function ProgressBar({ step, style }: Props) {
    return (
        <View style={[styles.row, style]}>
            <View style={[styles.dash, step >= 1 && styles.dashFilled]} />
            <View style={[styles.dash, step >= 2 && styles.dashFilled]} />
            <View style={[styles.dash, step >= 3 && styles.dashFilled]} />
        </View>
    );
}

const styles = StyleSheet.create({
    row: {
        flexDirection: "row",
        gap: 8,
    },
    dash: {
        // width: 8,
        flex: 1,
        height: 4,
        borderRadius: 2,
        backgroundColor: colors.border,
    },
    dashFilled: {
        backgroundColor: colors.sage,
    },
});
