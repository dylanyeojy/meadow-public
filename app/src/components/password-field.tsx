import {
    StyleSheet,
    Text,
    TextInput,
    TextInputProps,
    View,
} from "react-native";
import { colors, type, inputFont } from "@/theme";
import { useState } from "react";
import * as icon from "@/components/icons";
import { PressableScale } from "@/components/pressable-scale";

type Props = TextInputProps & { label: string; hint?: string; error?: string };

export function PasswordField({ label, hint, error, ...rest }: Props) {
    const [passwordVisible, setPasswordVisible] = useState(false);

    return (
        <View>
            <Text style={styles.label}>{label}</Text>
            <View style={styles.passwordBox}>
                <TextInput
                    style={
                        passwordVisible
                            ? [styles.passwordInput, { letterSpacing: 1 }]
                            : styles.passwordInput
                    }
                    secureTextEntry={!passwordVisible}
                    {...rest}
                />
                <PressableScale
                    style={styles.eyeTap}
                    onPress={() => setPasswordVisible(!passwordVisible)}
                >
                    {passwordVisible ? (
                        <icon.EyeOnIcon color={colors.sage} size={20} />
                    ) : (
                        <icon.EyeOffIcon color={colors.sage} size={20} />
                    )}
                </PressableScale>
            </View>
            {error ? (
                <Text style={styles.error}>{error}</Text>
            ) : (
                hint && <Text style={styles.passwordHint}>{hint}</Text>
            )}
        </View>
    );
}

const styles = StyleSheet.create({
    label: {
        ...type.subhead,
        fontWeight: "500",
        color: colors.muted,
        marginBottom: 7,
    },
    passwordBox: {
        flexDirection: "row",
        alignItems: "center",
        backgroundColor: colors.surface,
        borderWidth: 1,
        borderColor: colors.border,
        borderRadius: 16,
        paddingVertical: 15,
        paddingHorizontal: 16,
    },
    passwordInput: {
        flex: 1,
        padding: 0,
        fontFamily: inputFont,
        fontSize: type.body.fontSize,
        color: colors.ink,
        letterSpacing: 3,
    },
    eyeTap: {
        width: 44,
        height: 44,
        marginVertical: -14,
        marginRight: -6,
        justifyContent: "center",
        alignItems: "center",
    },
    passwordHint: {
        ...type.caption,
        fontWeight: "400",
        color: colors.muted,
        marginTop: 7,
    },
    error: {
        ...type.footnote,
        fontWeight: "500",
        color: colors.destructive,
        marginTop: 7,
    },
});
