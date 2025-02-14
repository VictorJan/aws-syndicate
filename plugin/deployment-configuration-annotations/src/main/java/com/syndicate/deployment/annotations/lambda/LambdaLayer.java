/*
 * Copyright 2018 EPAM Systems, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package com.syndicate.deployment.annotations.lambda;

import com.syndicate.deployment.annotations.DeploymentResource;
import com.syndicate.deployment.model.ArtifactExtension;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

/**
 * Created by Oleksandr Onsha on 2019-11-29
 */
@DeploymentResource
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
public @interface LambdaLayer {

	String layerName();

	String description() default  "";

	String layerFileName() default "";

	String licence() default "";

	ArtifactExtension artifactExtension() default ArtifactExtension.ZIP;

}
