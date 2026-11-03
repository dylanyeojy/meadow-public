import {
    StyleSheet,
    Text,
    TextInput,
    TextInputProps,
    View,
} from "react-native";
import { colors, type, inputFont } from "@/theme";

type Props = TextInputProps & { label: string; error?: string };

export function InputField({ label, error, ...rest }: Props) {
    return (
        <View>
            <Text style={styles.label}>{label}</Text>
            <TextInput style={styles.input} {...rest} />
            {error && <Text style={styles.error}>{error}</Text>}
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
    input: {
        backgroundColor: colors.surface,
        borderWidth: 1,
        borderColor: colors.border,
        borderRadius: 16,
        paddingVertical: 15,
        paddingHorizontal: 16,
        fontFamily: inputFont,
        fontSize: type.body.fontSize,
        color: colors.ink,
    },
    error: {
        ...type.footnote,
        fontWeight: "500",
        color: colors.destructive,
        marginTop: 7,
    },
});
