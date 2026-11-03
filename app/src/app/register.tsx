import {
    View,
    StyleSheet,
    Text,
    KeyboardAvoidingView,
    Image,
    ScrollView,
} from "react-native";
import { useState } from "react";
import { SafeAreaView } from "react-native-safe-area-context";
import { type, colors } from "@/theme";
import { router } from "expo-router";
import { PressableScale } from "@/components/pressable-scale";
import { PrimaryButton } from "@/components/primary-button";
import { InputField } from "@/components/input-field";
import { PasswordField } from "@/components/password-field";

export default function RegisterScreen() {
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [submitted, setSubmitted] = useState(false);
    const emailLooksValid = /^\S+@\S+\.\S+$/.test(email.trim());

    const nameError =
        submitted && name.trim() === "" ? "Enter your name." : undefined;
    const emailError =
        submitted && !emailLooksValid ? "Enter a valid email." : undefined;
    const passwordError =
        submitted && password.length < 8
            ? "Use at least 8 characters."
            : undefined;

    function handleCreateAccount() {
        setSubmitted(true);
        if (name.trim() === "" || !emailLooksValid || password.length < 8)
            return;
        router.replace("/onboarding/welcome");
    }
    return (
        <SafeAreaView style={styles.screen}>
            <KeyboardAvoidingView style={styles.keyboard} behavior="padding">
                <ScrollView
                    contentContainerStyle={styles.middle}
                    keyboardShouldPersistTaps="handled"
                    showsVerticalScrollIndicator={false}
                >
                    <View style={styles.header}>
                        <Text style={styles.title}>Create your account</Text>
                        <Text style={styles.subtitle}>
                            A private space, just for you.
                        </Text>
                    </View>
                    {/* Form Inputs */}
                    <View style={styles.form}>
                        <InputField
                            label="Full name"
                            autoCapitalize="words"
                            autoComplete="name"
                            value={name}
                            onChangeText={setName}
                            error={nameError}
                        />
                        <InputField
                            label="Email"
                            autoCapitalize="none"
                            autoComplete="email"
                            keyboardType="email-address"
                            value={email}
                            onChangeText={setEmail}
                            error={emailError}
                        />

                        <PasswordField
                            label="Password"
                            hint="At least 8 characters."
                            value={password}
                            onChangeText={setPassword}
                            error={passwordError}
                        />

                        <PrimaryButton
                            label="Create account"
                            onPress={handleCreateAccount}
                            style={{ marginTop: 4 }}
                        />

                        <View style={styles.dividerRow}>
                            <View style={styles.dividerLine} />
                            <Text style={styles.dividerText}>or</Text>
                            <View style={styles.dividerLine} />
                        </View>

                        <PressableScale
                            style={[styles.googleButton]}
                            onPress={() =>
                                router.replace("/onboarding/welcome")
                            }
                        >
                            <Image
                                source={require("@/assets/images/google-logo.png")}
                                style={styles.googleLogo}
                            />
                            <Text style={[styles.googleText]}>
                                Sign up with Google
                            </Text>
                        </PressableScale>
                    </View>
                </ScrollView>
            </KeyboardAvoidingView>
            <View style={styles.footer}>
                <Text style={styles.footerText}>Already have an account?</Text>
                <PressableScale
                    onPress={() =>
                        router.back()
                    } /* change this to register screen later*/
                    hitSlop={{ top: 14, bottom: 14, left: 8, right: 8 }}
                >
                    <Text style={styles.footerLink}>Log in</Text>
                </PressableScale>
            </View>
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
    screen: {
        flex: 1,
        backgroundColor: colors.sand,
        paddingHorizontal: 24,
    },
    middle: {
        flexGrow: 1,
        justifyContent: "center",
    },
    footer: {
        justifyContent: "center",
        paddingTop: 24,
        paddingBottom: 30,
        flexDirection: "row",
        gap: 4,
        alignItems: "baseline",
    },
    footerText: {
        ...type.subhead,
        fontWeight: "400",
        color: colors.muted,
    },
    footerLink: {
        ...type.subhead,
        fontWeight: "700",
        color: colors.sage,
    },
    header: {
        marginBottom: 28,
    },
    title: {
        ...type.largeTitle,
        color: colors.ink,
        lineHeight: 39,
    },
    subtitle: {
        ...type.body,
        marginTop: 4,
        color: colors.muted,
    },
    form: {
        gap: 16,
    },
    keyboard: {
        flex: 1,
    },
    dividerRow: {
        flexDirection: "row",
        alignItems: "center",
        gap: 12,
        marginVertical: 6,
    },
    dividerLine: {
        flex: 1,
        height: 1,
        backgroundColor: colors.border,
    },
    dividerText: {
        ...type.caption,
        color: colors.muted,
        fontWeight: "400",
        fontSize: 12,
        includeFontPadding: false,
        top: -1.5,
    },
    googleButton: {
        backgroundColor: colors.surface,
        borderRadius: 16,
        paddingVertical: 14,
        alignItems: "center",
        justifyContent: "center",
        flexDirection: "row",
        gap: 10,
        borderColor: colors.border,
        borderWidth: 1,
    },
    googleText: {
        ...type.headline,
        color: colors.ink,
        textAlign: "center",
        includeFontPadding: false,
        fontSize: 16,
    },
    googleLogo: {
        width: 20,
        height: 20,
        // top: -1,
    },
});
