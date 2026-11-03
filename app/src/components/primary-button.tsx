import { StyleProp, StyleSheet, Text, ViewStyle } from "react-native";
import { PressableScale } from "@/components/pressable-scale";
import { colors, type } from "@/theme";

type Props = {
    label: string;
    onPress: () => void;
    style?: StyleProp<ViewStyle>;
    disabled?: boolean;
};

export function PrimaryButton({ label, onPress, style, disabled }: Props) {
    return (
        <PressableScale
            style={[styles.button, disabled && styles.buttonDisabled, style]}
            onPress={onPress}
            disabled={disabled}
        >
            <Text style={[styles.text, disabled && styles.textDisabled]}>
                {label}
            </Text>
        </PressableScale>
    );
}

const styles = StyleSheet.create({
    button: {
        backgroundColor: colors.sage,
        borderRadius: 16,
        paddingVertical: 16,
        alignItems: "center",
    },
    text: {
        ...type.headline,
        color: colors.surface,
        textAlign: "center",
        includeFontPadding: false,
    },
    buttonDisabled: {
        backgroundColor: colors.disabledFill,
    },
    textDisabled: {
        color: colors.disabledInk,
    },
});
